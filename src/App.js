import { useState, useEffect } from 'react';
import EditableBoardTitle from './components/EditableBoardTitle';

const App = () => {
  // app -> (EditableBoardTitle -> (BoardEditFormModal + BoardDeleteFormModal)) + (JobList -> Job) + AddJobButton

  const [boardTitle, setBoardTitle] = useState('');

  useEffect(() => {
    setBoardTitle('Jobs');
  }, []);

  return (
    <h1>{ boardTitle }</h1>
  );
}

export default App;