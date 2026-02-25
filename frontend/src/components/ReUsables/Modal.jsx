import warningGif from "../../assets/gifs/warning.gif";
import successGif from "../../assets/gifs/success.gif"


const Modal = ({ image, title, desc, descNode, children, opened }) => {
  if (!opened) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="relative w-full max-w-2xl bg-white p-6 mx-4">
        <div className="w-full space-y-2 text-center">
          <div className="">
            {image && (
              <img
                className="mx-auto max-w-55 max-h-55"
                src={
                  {
                    successGif,
                    warningGif,
                  }[image] || image
                }
                alt="status"
              />
            )}
          </div>

          <div className="">
            {title && (
              <p className="typo-xl">
                {title}
              </p>
            )}

            {desc ? (
              <p className="typo-base">{desc}</p>
            ) : (
              descNode
            )}
          </div>

          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
