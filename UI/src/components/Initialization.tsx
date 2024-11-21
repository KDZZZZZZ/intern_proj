import React, { useState } from "react";

const Initialization: React.FC = () => {
  const [keywords, setKeywords] = useState<string[]>([]);
  const [selectedScenario, setSelectedScenario] = useState<string>("");

  const handleAddKeyword = (keyword: string) => {
    setKeywords([...keywords, keyword]);
  };

  return (
    <div>
      <h2>用户初始化界面</h2>
      <div>
        <h3>输入人格特征关键词</h3>
        <input
          type="text"
          placeholder="输入关键词"
          onKeyDown={(e) => {
            if (e.key === "Enter" && e.currentTarget.value.trim()) {
              handleAddKeyword(e.currentTarget.value.trim());
              e.currentTarget.value = "";
            }
          }}
        />
        <div>
          <strong>关键词:</strong> {keywords.join(", ")}
        </div>
      </div>
      <div>
        <h3>选择情节</h3>
        <select
          value={selectedScenario}
          onChange={(e) => setSelectedScenario(e.target.value)}
        >
          <option value="">请选择</option>
          <option value="scenario1">情节1</option>
          <option value="scenario2">情节2</option>
          <option value="scenario3">情节3</option>
        </select>
        <div>
          <strong>已选情节:</strong> {selectedScenario}
        </div>
      </div>
    </div>
  );
};

export default Initialization;
