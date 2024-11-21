import React, { useState } from "react";

interface MoodVAD {
  valence: number;
  arousal: number;
  dominance: number;
}

const DailyInteraction: React.FC = () => {
  const [mood, setMood] = useState<MoodVAD>({
    valence: 0.5,
    arousal: 0.5,
    dominance: 0.5,
  });
  const [dialogue, setDialogue] = useState<string>("");
  const [favorability, setFavorability] = useState<number>(50); // 0-100

  const handleMoodChange = (field: keyof MoodVAD, value: number) => {
    setMood({ ...mood, [field]: value });
  };

  return (
    <div>
      <h2>用户日常交互界面</h2>

      {/* Mood VAD 状态栏 */}
      <div>
        <h3>Mood VAD 状态栏</h3>
        {["valence", "arousal", "dominance"].map((field) => (
          <div key={field}>
            <label>{field}</label>
            <input
              type="range"
              min={0}
              max={1}
              step={0.01}
              value={mood[field as keyof MoodVAD]}
              onChange={(e) =>
                handleMoodChange(field as keyof MoodVAD, parseFloat(e.target.value))
              }
            />
            <span>{mood[field as keyof MoodVAD].toFixed(2)}</span>
          </div>
        ))}
      </div>

      {/* 对话框 */}
      <div>
        <h3>对话框</h3>
        <input
          type="text"
          placeholder="输入对话"
          value={dialogue}
          onChange={(e) => setDialogue(e.target.value)}
        />
        <div>
          <strong>当前对话:</strong> {dialogue}
        </div>
      </div>

      {/* 好感度状态栏 */}
      <div>
        <h3>好感度状态栏</h3>
        <input
          type="range"
          min={0}
          max={100}
          step={1}
          value={favorability}
          onChange={(e) => setFavorability(parseInt(e.target.value))}
        />
        <span>{favorability}</span>
      </div>
    </div>
  );
};

export default DailyInteraction;
