import type { DailyMission, UnlockedAchievementInfo, UnlockedTitleInfo } from '../types/api'
import client from './client'

export interface ClaimMissionResponse {
  code: string
  claimed: boolean
  reward_cultivation_power: number
  reward_reputation: number
  new_cultivation_power: number
  new_reputation: number
  unlocked_achievements: UnlockedAchievementInfo[]
  unlocked_titles: UnlockedTitleInfo[]
}

export async function getDailyMissions(): Promise<DailyMission[]> {
  const res = await client.get<{ missions: DailyMission[] }>('/quests/daily')
  return res.data.missions
}

export async function claimMission(missionCode: string): Promise<ClaimMissionResponse> {
  const res = await client.post<ClaimMissionResponse>(`/quests/daily/${missionCode}/claim`)
  return res.data
}
