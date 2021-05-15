import { useState, useEffect } from "react";
import EditableBoardTitle from "./components/EditableBoardTitle";

const App = () => {
  // app -> (EditableBoardTitle -> (BoardEditFormModal + BoardDeleteFormModal)) + (JobList -> Job) + AddJobButton

  const [boardTitle, setBoardTitle] = useState("");

  useEffect(() => {
    setBoardTitle("Jobs");
  }, []);

  return (
    <div className="container-fluid cpx-0 pt-3" id="container">
      <div className="row no-gutters justify-content-between align-items-center mb-3">
        <EditableBoardTitle title={boardTitle} />
      </div>
      <div className="row flex-row flex-nowrap overflow-y-hidden">
        {/* <JobList /> */}
      </div>
    </div>
  );
};

export default App;
