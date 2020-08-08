import React, { useState, useEffect } from 'react';

export default function LoadingTextAnim(props) {
  const MAX_PERIODS = 3;
  const BASE_TEXT = "Loading";

  const [numPeriods, setNumPeriods] = useState(1);
  const [text, setText] = useState(BASE_TEXT);

  useEffect(() => {
    var scheduler = setTimeout(() => {
      setNumPeriods(((numPeriods) % MAX_PERIODS) + 1);
      var new_text = BASE_TEXT;
      for(var i = 0; i < numPeriods; i++) {
        new_text += ".";
      }
      setText(new_text);
    }, props.speed);

    return () => {
      clearTimeout(scheduler); 
    }
  });

  return(
    <h1 id="LoadingText">
      {text}
    </h1>
  );
}

LoadingTextAnim.defaultProps = {speed: 500};
