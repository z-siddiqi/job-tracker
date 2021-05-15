import { BsPencil } from "react-icons/bs";
import { BsTrash } from "react-icons/bs";

const EditableBoardTitle = (props) => {
  return (
    <>
      <div className="text-truncate" style={{ flex: 1 }}>
        <h3>{props.title}</h3>
      </div>
      <div className="d-flex text-nowrap ml-2">
        <h4 className="cursor-pointer">
          <BsPencil />
        </h4>
        <h4 className="cursor-pointer ml-2">
          <BsTrash />
        </h4>
      </div>
    </>
  );
};

export default EditableBoardTitle;
