import { useState, useEffect } from "react";
import { Modal, Form, Button } from "react-bootstrap";

const BoardEditFormModal = (props) => {
  const [title, setTitle] = useState("");

  useEffect(() => {
    setTitle(props.initialTitle);
  }, [props.initialTitle]);

  const handleTitleChange = (e) => {
    setTitle(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
  };

  return (
    <>
      <Modal show={props.isOpen} onHide={props.onClose}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Board</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="title">
              <Form.Label>Title</Form.Label>
              <Form.Control
                type="text"
                value={title}
                onChange={handleTitleChange}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button type="submit" variant="dark">
            Edit
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default BoardEditFormModal;
