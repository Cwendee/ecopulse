import clsx from "clsx";
import { BiLoader } from "react-icons/bi";

export const Button = ({
  children,
  variant = "primary",
  size = "md",
  leftSection,
  rightSection,
  fullWidth = false,
  disabled = false,
  loading = false,
  className,
  ...props
}) => {
  return (
    <button
      className={clsx(
        "btn",
        `btn--${variant}`,
        `btn--${size}`,
        {
          "btn--full-width": fullWidth,
          "btn--disabled": disabled,
          "btn--loading": loading,
        },
        className,
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <span className="btn__loader">
          <BiLoader />
        </span>
      ) : (
        <>
          {leftSection && (
            <span className="btn__left-section">{leftSection}</span>
          )}

          <span className="btn__content">{children}</span>

          {rightSection && (
            <span className="btn__right-section">{rightSection}</span>
          )}
        </>
      )}
    </button>
  );
};

export default Button;
