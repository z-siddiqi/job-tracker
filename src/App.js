import { useState, useEffect } from "react";
import EditableBoardTitle from "./components/EditableBoardTitle";
import BoardEditFormModal from "./components/BoardEditFormModal";
import BoardDeleteFormModal from "./components/BoardDeleteFormModal";

const App = () => {
  // app -> (EditableBoardTitle -> (BoardEditFormModal + BoardDeleteFormModal)) + (JobList -> Job) + AddJobButton

  const [boardTitle, setBoardTitle] = useState("");
  const [isEditFormOpen, setIsEditFormOpen] = useState(false);
  const [isDeleteFormOpen, setIsDeleteFormOpen] = useState(false);

  useEffect(() => {
    setBoardTitle("Jobs");
  }, []);

  const handleEditFormOpen = () => {
    setIsEditFormOpen(true);
  };

  const handleEditFormClose = () => {
    setIsEditFormOpen(false);
  };

  const handleEditFormSubmit = (attrs) => {
    updateBoard(attrs);
    setIsEditFormOpen(false);
  };

  const updateBoard = (attrs) => {
    setBoardTitle(attrs.title);
  };

  const handleDeleteFormOpen = () => {
    setIsDeleteFormOpen(true);
  };

  const handleDeleteFormClose = () => {
    setIsDeleteFormOpen(false);
  };

  const handleDeleteFormSubmit = () => {
    setIsDeleteFormOpen(false);
  };

  return (
    <div className="container-fluid cpx-0 pt-3" id="container">
      <div className="row no-gutters align-items-center mb-3">
        <EditableBoardTitle
          title={boardTitle}
          onEditClick={handleEditFormOpen}
          onDeleteClick={handleDeleteFormOpen}
        />
      </div>
      <div className="row flex-row flex-nowrap overflow-y-hidden">
        {/* <JobList /> */}
      </div>
      <BoardEditFormModal
        initialTitle={boardTitle}
        isOpen={isEditFormOpen}
        onClose={handleEditFormClose}
        onSubmit={handleEditFormSubmit}
      />
      <BoardDeleteFormModal
        isOpen={isDeleteFormOpen}
        onClose={handleDeleteFormClose}
        onSubmit={handleDeleteFormSubmit}
      />
    </div>
  );
};

export default App;
