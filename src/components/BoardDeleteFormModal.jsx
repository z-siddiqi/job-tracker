import { Modal, Button } from "react-bootstrap";

const BoardDeleteFormModal = (props) => {
  const handleSubmit = () => {
    props.onSubmit();
  };

  return (
    <>
      <Modal show={props.isOpen} onHide={props.onClose}>
        <Modal.Header closeButton>
          <Modal.Title>Delete Board</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="lead">Are you sure you want to delete this board?</p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger" onClick={handleSubmit}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default BoardDeleteFormModal;
