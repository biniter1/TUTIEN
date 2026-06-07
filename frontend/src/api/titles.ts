import type { Title } from '../types/api'
import client from './client'

export interface EquipTitleResponse {
  code: string
  name: string
  rarity: string
  is_equipped: boolean
}

export async function getMyTitles(): Promise<Title[]> {
  const res = await client.get<{ titles: Title[] }>('/titles/me')
  return res.data.titles
}

export async function equipTitle(titleCode: string): Promise<EquipTitleResponse> {
  const res = await client.post<EquipTitleResponse>(`/titles/${titleCode}/equip`)
  return res.data
}
