import warningGif from "../../assets/gifs/warning.gif";
import successGif from "../../assets/gifs/success.gif";

const Modal = ({
  image,
  title,
  desc,
  descNode,
  children,
  opened,
  onClose,
  bgColor = "#296083",
}) => {
  if (!opened) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-3xl p-6 mx-4"
        onClick={(e) => e.stopPropagation()}
        style={{ backgroundColor: bgColor }}
      >
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-black rounded-full w-6 h-6 bg-white"
        >
          ✕
        </button>

        <div className="w-full space-y-2 text-center">
          {image && (
            <img
              className="mx-auto max-w-55 max-h-55"
              src={{ successGif, warningGif }[image] || image}
              alt="status"
            />
          )}

          {title && <p className="typo-xl">{title}</p>}

          {desc ? <p className="typo-base">{desc}</p> : descNode}

          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
