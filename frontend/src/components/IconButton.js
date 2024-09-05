import React from 'react';

const IconButton = ({
  'aria-label': ariaLabel,
  children,
  className,
  disabled,
  onClick,
  ...rest
}) => {
  return (
    <button
      aria-label={ariaLabel}
      className={`icon-button ${className || ''}`}
      disabled={disabled}
      onClick={onClick}
      {...rest}
    >
      {children}
    </button>
  );
};

export default IconButton;