import { useState, useEffect } from "react";
import EditableBoardTitle from "./components/EditableBoardTitle";
import BoardEditFormModal from "./components/BoardEditFormModal";

const App = () => {
  // app -> (EditableBoardTitle -> (BoardEditFormModal + BoardDeleteFormModal)) + (JobList -> Job) + AddJobButton

  const [boardTitle, setBoardTitle] = useState("");
  const [isEditFormOpen, setIsEditFormOpen] = useState(false);

  useEffect(() => {
    setBoardTitle("Jobs");
  }, []);

  const handleEditFormOpen = () => {
    setIsEditFormOpen(true);
  };

  const handleEditFormClose = () => {
    setIsEditFormOpen(false);
  };

  return (
    <div className="container-fluid cpx-0 pt-3" id="container">
      <div className="row no-gutters align-items-center mb-3">
        <EditableBoardTitle title={boardTitle} onEditClick={handleEditFormOpen} />
      </div>
      <div className="row flex-row flex-nowrap overflow-y-hidden">
        {/* <JobList /> */}
      </div>
      <BoardEditFormModal
        initialTitle={boardTitle}
        isOpen={isEditFormOpen}
        onClose={handleEditFormClose}
      />
    </div>
  );
};

export default App;
