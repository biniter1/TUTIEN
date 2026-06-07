import type { CultivationProfile } from '../types/api'
import client from './client'

export async function getMyProfile(): Promise<CultivationProfile> {
  const res = await client.get<CultivationProfile>('/cultivation/me')
  return res.data
}
