import type { QuizSubmitResponse, SetProgress, VocabularySet, VocabularyWord, WordProgress } from '../types/api'
import client from './client'

export async function getSets(): Promise<VocabularySet[]> {
  const res = await client.get<{ sets: VocabularySet[] }>('/vocabulary/sets')
  return res.data.sets
}

export async function getSetDetail(setId: string): Promise<VocabularySet> {
  const res = await client.get<VocabularySet>(`/vocabulary/sets/${setId}`)
  return res.data
}

export async function getWords(setId: string): Promise<VocabularyWord[]> {
  const res = await client.get<{ words: VocabularyWord[] }>(`/vocabulary/sets/${setId}/words`)
  return res.data.words
}

export async function submitQuiz(
  wordId: string,
  quizType: string,
  answer: string,
): Promise<QuizSubmitResponse> {
  const res = await client.post<QuizSubmitResponse>('/vocabulary/quiz/submit', {
    word_id: wordId,
    quiz_type: quizType,
    answer,
  })
  return res.data
}

export async function getMyProgress(): Promise<WordProgress[]> {
  const res = await client.get<{ progress: WordProgress[] }>('/vocabulary/progress/me')
  return res.data.progress
}

export async function getSetProgress(setId: string): Promise<SetProgress> {
  const res = await client.get<SetProgress>(`/vocabulary/sets/${setId}/progress`)
  return res.data
}
