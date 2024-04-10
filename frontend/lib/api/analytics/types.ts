interface Usage {
  date: Date;
  usage_count: number;
}

export interface BrainsUsages {
  usages: Usage[];
}

export enum Range {
  WEEK = 7,
  MONTH = 30,
  QUARTER = 90,
}
