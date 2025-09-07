import { Link, useLocation } from "react-router-dom";

export const LinkWithQuery = ({ children, to, ...props }) => {
  const { search } = useLocation();

  // Combine the 'to' prop with the current search params
  const combinedTo = `${to}${search}`;

  return (
    <Link to={combinedTo} {...props} aria-label="Navigation Link">
      {children}
    </Link>
  );
};
