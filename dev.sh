#!/bin/bash
# Dev mode: watchexec restarts realtime binary on Rust source changes
set -e

cd /root/f1-dash
source "$HOME/.cargo/env"

export ADDRESS=0.0.0.0:4001
export ORIGIN=http://31.220.72.155:3001
export F1_DEV_URL=ws://172.21.0.3:3001/ws
export RUST_LOG=realtime=info,warn

echo "Starting realtime dev server on :4001 (watching for changes)..."
echo "Frontend dev at http://31.220.72.155:3001"

watchexec \
  --watch realtime/src \
  --watch signalr/src \
  --exts rs \
  --restart \
  --on-busy-update restart \
  -- bash -c 'cargo build --bin realtime 2>&1 && ./target/debug/realtime'
