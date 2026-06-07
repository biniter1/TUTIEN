import type { Achievement } from '../types/api'
import client from './client'

export async function getMyAchievements(): Promise<Achievement[]> {
  const res = await client.get<{ achievements: Achievement[] }>('/achievements/me')
  return res.data.achievements
}
