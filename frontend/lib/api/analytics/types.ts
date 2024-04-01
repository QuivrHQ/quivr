interface Usage {
  date: Date;
  usageCount: number;
}

interface BrainUsages {
  brainId: string;
  usages: Usage[];
}

export interface BrainsUsages {
  brainsUsages: BrainUsages[];
}
