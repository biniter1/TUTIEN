export interface User {
  id: string
  email: string
  username: string
  dao_name: string | null
  is_active: boolean
  created_at: string
}

export interface CultivationProfile {
  user_id: string
  cultivation_power: number
  spirit_energy: number
  reputation: number
  realm: string
}

export interface VocabularySet {
  id: string
  code: string
  name: string
  description: string | null
}

export interface VocabularyWord {
  id: string
  set_id: string
  english: string
  vietnamese: string
  example_sentence: string | null
  pronunciation: string | null
}

export interface MissionProgressUpdate {
  code: string
  progress_value: number
  target_value: number
  is_completed: boolean
}

export interface UnlockedAchievementInfo {
  code: string
  name: string
  description: string | null
  reward_title_code: string | null
}

export interface UnlockedTitleInfo {
  code: string
  name: string
  rarity: string
}

export interface QuizSubmitResponse {
  word_id: string
  quiz_type: string
  is_correct: boolean
  correct_answer: string
  cultivation_power: number
  spirit_energy_spent: number
  remaining_spirit_energy: number
  correct_count: number
  wrong_count: number
  mastery_level: number
  daily_missions_updated: MissionProgressUpdate[]
  unlocked_achievements: UnlockedAchievementInfo[]
  unlocked_titles: UnlockedTitleInfo[]
}

export interface WordProgress {
  word_id: string
  correct_count: number
  wrong_count: number
  mastery_level: number
}

export interface SetProgress {
  set_id: string
  total_words: number
  practiced_words: number
  mastered_words: number
}

export interface DailyMission {
  code: string
  name: string
  description: string | null
  mission_type: string
  target_value: number
  reward_cultivation_power: number
  reward_reputation: number
  progress_value: number
  is_completed: boolean
  is_claimed: boolean
}

export interface Achievement {
  code: string
  name: string
  description: string | null
  category: string | null
  is_hidden: boolean
  is_unlocked: boolean
  unlocked_at: string | null
  reward_title_code: string | null
}

export interface Title {
  code: string
  name: string
  description: string | null
  rarity: string
  is_unlocked: boolean
  is_equipped: boolean
  unlocked_at: string | null
}
