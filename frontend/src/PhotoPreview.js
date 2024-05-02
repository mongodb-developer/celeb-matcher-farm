import "./PhotoPreview.css";

import React from "react";
import CircumIcon from "@klarr-agency/circum-icons-react";

function PhotoPreview({ imgSrc, onClick }) {
  const showing = imgSrc !== null;
  return (
    <div className="PhotoPreview">
      <div className={showing ? "frame showing" : "frame"}>
        <img src={imgSrc} className="image" alt="You, possibly." />
        <button className="upload" onClick={onClick}>
          Find Your Celebrity Lookalike!
        </button>
      </div>
    </div>
  );
}

export default PhotoPreview;
