import { create } from "zustand";

export type LapTimeEntry = {
	lap: number;
	time: string;
	ms: number;
	overallFastest: boolean;
	personalFastest: boolean;
};

type HistoryStore = {
	lapTimes: Record<string, LapTimeEntry[]>;
	positions: Record<number, Record<string, number>>;
	recordLapTime: (nr: string, lap: number, entry: Omit<LapTimeEntry, "lap">) => void;
	recordPositions: (lap: number, positions: Record<string, number>) => void;
	reset: () => void;
};

function parseTimeMs(time: string): number {
	const parts = time.split(":");
	if (parts.length === 2) {
		return (parseInt(parts[0]) * 60 + parseFloat(parts[1])) * 1000;
	}
	return parseFloat(time) * 1000;
}

export { parseTimeMs };

export const useHistoryStore = create<HistoryStore>((set, get) => ({
	lapTimes: {},
	positions: {},

	recordLapTime: (nr, lap, entry) => {
		const existing = get().lapTimes[nr] ?? [];
		if (existing.some((e) => e.lap === lap)) return;
		set((prev) => ({
			lapTimes: {
				...prev.lapTimes,
				[nr]: [...(prev.lapTimes[nr] ?? []), { lap, ...entry }],
			},
		}));
	},

	recordPositions: (lap, positions) => {
		if (get().positions[lap]) return;
		set((prev) => ({
			positions: { ...prev.positions, [lap]: positions },
		}));
	},

	reset: () => set({ lapTimes: {}, positions: {} }),
}));
