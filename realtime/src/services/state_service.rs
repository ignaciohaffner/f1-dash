use anyhow::Error;
use serde_json::{Value, json};
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Clone)]
pub struct StateService {
    state: Arc<RwLock<Value>>,
}

impl StateService {
    pub fn new() -> Self {
        Self {
            state: Arc::new(RwLock::new(Value::Object(serde_json::Map::new()))),
        }
    }

    pub async fn get_state(&self) -> Result<Value, Error> {
        let state = self.state.read().await;
        Ok(state.clone())
    }

    pub async fn get_state_string(&self) -> Result<String, Error> {
        let state = self.state.read().await;
        Ok(state.to_string())
    }

    pub async fn set_state(&self, new_state: Value) -> Result<(), Error> {
        let mut state = self.state.write().await;
        *state = new_state;
        Ok(())
    }

    pub async fn update_state(&self, update: Value) -> Result<(), Error> {
        let mut state = self.state.write().await;

        // Detect lap completions and accumulate LapHistory before merging
        if let Some(Value::Object(lines)) = update.pointer("/TimingData/Lines") {
            for (nr, driver_update) in lines {
                let new_laps = match driver_update.pointer("/NumberOfLaps").and_then(Value::as_u64) {
                    Some(v) => v,
                    None => continue,
                };

                let current_laps = state
                    .pointer(&format!("/TimingData/Lines/{}/NumberOfLaps", nr))
                    .and_then(Value::as_u64)
                    .unwrap_or(0);

                if new_laps <= current_laps {
                    continue;
                }

                // Prefer lap time from the update, fall back to current state
                let time = driver_update
                    .pointer("/LastLapTime/Value")
                    .or_else(|| state.pointer(&format!("/TimingData/Lines/{}/LastLapTime/Value", nr)))
                    .and_then(Value::as_str)
                    .unwrap_or("")
                    .to_string();

                if time.is_empty() || time.contains("LAP") {
                    continue;
                }

                let overall_fastest = driver_update
                    .pointer("/LastLapTime/OverallFastest")
                    .and_then(Value::as_bool)
                    .unwrap_or(false);

                let personal_fastest = driver_update
                    .pointer("/LastLapTime/PersonalFastest")
                    .and_then(Value::as_bool)
                    .unwrap_or(false);

                let entry = json!({
                    "lap": new_laps,
                    "time": time,
                    "overallFastest": overall_fastest,
                    "personalFastest": personal_fastest,
                });

                // Ensure LapHistory object exists
                if state.get("LapHistory").is_none() {
                    if let Some(obj) = state.as_object_mut() {
                        obj.insert("LapHistory".to_string(), Value::Object(Default::default()));
                    }
                }

                // Ensure driver array exists and push entry
                if let Some(lap_history) = state.get_mut("LapHistory").and_then(Value::as_object_mut) {
                    lap_history
                        .entry(nr.clone())
                        .or_insert_with(|| Value::Array(vec![]))
                        .as_array_mut()
                        .unwrap()
                        .push(entry);
                }
            }
        }

        merge(&mut state, update);
        Ok(())
    }
}

pub fn merge(base: &mut Value, update: Value) {
    match (base, update) {
        (Value::Object(prev), Value::Object(update)) => {
            for (k, v) in update {
                merge(prev.entry(k).or_insert(Value::Null), v);
            }
        }
        (Value::Array(prev), Value::Object(update)) => {
            for (k, v) in update {
                if let Ok(index) = k.parse::<usize>() {
                    if let Some(item) = prev.get_mut(index) {
                        merge(item, v);
                    } else {
                        prev.push(v);
                    }
                }
            }
        }
        (a, b) => *a = b,
    }
}
