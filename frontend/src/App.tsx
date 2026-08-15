import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

type Exam = {
  exam_id: string;
  name: string;
  description: string;
};

type Subject = {
  subject_id: string;
  exam_id: string;
  name: string;
  description: string;
};

type Chapter = {
  chapter_id: string;
  subject_id: string;
  exam_id: string;
  name: string;
};

type Question = {
  question_id: string;
  text: string;
  options: string[];
  position: number;
};

type QuizResponse = {
  quiz_id: string;
  user_id: string;
  questions: Question[];
};

type Result = {
  quiz_id: string;
  user_id: string;
  total_questions: number;
  correct_answers: number;
  score_percentage: number;
};

type Screen =
  | "login"
  | "exams"
  | "subjects"
  | "chapters"
  | "quiz"
  | "result";

function App() {
  const [screen, setScreen] = useState<Screen>("login");
  const [userId, setUserId] = useState("user_001");

  const [exams, setExams] = useState<Exam[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [chapters, setChapters] = useState<Chapter[]>([]);

  const [selectedExam, setSelectedExam] = useState<Exam | null>(null);
  const [selectedSubject, setSelectedSubject] =
    useState<Subject | null>(null);
  const [selectedChapter, setSelectedChapter] =
    useState<Chapter | null>(null);

  const [quiz, setQuiz] = useState<QuizResponse | null>(null);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [questionShownAt, setQuestionShownAt] =
    useState<string>("");

  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function api<T>(path: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_URL}${path}`, {
      headers: {
        "Content-Type": "application/json",
      },
      ...options,
    });

    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.detail || "Request failed");
    }

    return response.json();
  }

  async function login() {
    setError("");
    setLoading(true);

    try {
      const data = await api<Exam[]>("/api/exams");
      setExams(data);
      setScreen("exams");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load exams");
    } finally {
      setLoading(false);
    }
  }

  async function selectExam(exam: Exam) {
    setError("");
    setLoading(true);

    try {
      const data = await api<Subject[]>(
        `/api/exams/${exam.exam_id}/subjects`,
      );

      setSelectedExam(exam);
      setSubjects(data);
      setScreen("subjects");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load subjects");
    } finally {
      setLoading(false);
    }
  }

  async function selectSubject(subject: Subject) {
    setError("");
    setLoading(true);

    try {
      const data = await api<Chapter[]>(
        `/api/subjects/${subject.subject_id}/chapters`,
      );

      setSelectedSubject(subject);
      setChapters(data);
      setScreen("chapters");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load chapters");
    } finally {
      setLoading(false);
    }
  }

  async function selectChapter(chapter: Chapter) {
    setError("");
    setLoading(true);

    try {
      const data = await api<QuizResponse>(
        `/api/quiz/${chapter.chapter_id}?user_id=${userId}`,
      );

      setSelectedChapter(chapter);
      setQuiz(data);
      setQuestionIndex(0);
      setSelectedOption(null);
      setQuestionShownAt(new Date().toISOString());
      setScreen("quiz");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load quiz");
    } finally {
      setLoading(false);
    }
  }

  async function submitAnswer() {
    if (!quiz || selectedOption === null) {
      return;
    }

    const question = quiz.questions[questionIndex];

    setError("");
    setLoading(true);

    try {
      await api("/api/quiz/submit", {
        method: "POST",
        body: JSON.stringify({
          user_id: userId,
          quiz_id: quiz.quiz_id,
          question_id: question.question_id,
          selected_option: selectedOption,
          question_shown_at: questionShownAt,
        }),
      });

      const isLastQuestion =
        questionIndex === quiz.questions.length - 1;

      if (isLastQuestion) {
        const finalResult = await api<Result>(
          `/api/quiz/${quiz.quiz_id}/result?user_id=${userId}`,
        );

        setResult(finalResult);
        setScreen("result");
      } else {
        setQuestionIndex((current) => current + 1);
        setSelectedOption(null);
        setQuestionShownAt(new Date().toISOString());
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to submit answer");
    } finally {
      setLoading(false);
    }
  }

  function restart() {
    setSelectedExam(null);
    setSelectedSubject(null);
    setSelectedChapter(null);
    setQuiz(null);
    setResult(null);
    setQuestionIndex(0);
    setSelectedOption(null);
    setScreen("exams");
  }

  const currentQuestion = quiz?.questions[questionIndex];

  return (
    <main className="app">
      <div className="container">
        <header>
          <h1>SkillBytes Quiz</h1>
          <p className="subtitle">AI-powered learning assessment</p>
        </header>

        {error && <div className="error">{error}</div>}

        {loading && <div className="loading">Loading...</div>}

        {screen === "login" && (
          <section className="card">
            <h2>Welcome</h2>
            <p>Select a predefined student to begin.</p>

            <select
              value={userId}
              onChange={(event) => setUserId(event.target.value)}
            >
              {Array.from({ length: 10 }, (_, index) => {
                const id = `user_${String(index + 1).padStart(3, "0")}`;

                return (
                  <option key={id} value={id}>
                    Student {String(index + 1).padStart(3, "0")}
                  </option>
                );
              })}
            </select>

            <button onClick={login}>Start</button>
          </section>
        )}

        {screen === "exams" && (
          <Selection
            title="Choose an Exam"
            items={exams}
            label={(exam) => exam.name}
            onSelect={selectExam}
          />
        )}

        {screen === "subjects" && (
          <Selection
            title={selectedExam?.name ?? "Choose a Subject"}
            items={subjects}
            label={(subject) => subject.name}
            onSelect={selectSubject}
          />
        )}

        {screen === "chapters" && (
          <Selection
            title={selectedSubject?.name ?? "Choose a Chapter"}
            items={chapters}
            label={(chapter) => chapter.name}
            onSelect={selectChapter}
          />
        )}

        {screen === "quiz" && currentQuestion && (
          <section className="card">
            <div className="progress">
              Question {questionIndex + 1} of {quiz?.questions.length}
            </div>

            <h2>{currentQuestion.text}</h2>

            <div className="options">
              {currentQuestion.options.map((option, index) => (
                <button
                  key={option}
                  className={
                    selectedOption === index ? "option selected" : "option"
                  }
                  onClick={() => setSelectedOption(index)}
                >
                  {option}
                </button>
              ))}
            </div>

            <button
              disabled={selectedOption === null || loading}
              onClick={submitAnswer}
            >
              {questionIndex === (quiz?.questions.length ?? 1) - 1
                ? "Finish Quiz"
                : "Next"}
            </button>
          </section>
        )}

        {screen === "result" && result && (
          <section className="card result">
            <h2>Quiz Complete!</h2>

            <div className="score">
              {result.score_percentage}%
            </div>

            <p>
              You answered {result.correct_answers} of{" "}
              {result.total_questions} questions correctly.
            </p>

            <button onClick={restart}>Take Another Quiz</button>
          </section>
        )}
      </div>
    </main>
  );
}

type SelectionProps<T> = {
  title: string;
  items: T[];
  label: (item: T) => string;
  onSelect: (item: T) => void;
};

function Selection<T>({
  title,
  items,
  label,
  onSelect,
}: SelectionProps<T>) {
  return (
    <section className="card">
      <h2>{title}</h2>

      <div className="selection-list">
        {items.map((item, index) => (
          <button
            key={index}
            className="selection"
            onClick={() => onSelect(item)}
          >
            {label(item)}
          </button>
        ))}
      </div>
    </section>
  );
}

export default App;