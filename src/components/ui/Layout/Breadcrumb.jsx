import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const Breadcrumb = ({ className = '' }) => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);

  return (
    <nav aria-label="breadcrumb" className={`flex items-center text-xs font-semibold text-ui-text-tertiary select-none ${className}`}>
      <ol className="inline-flex items-center space-x-1 md:space-x-2">
        <li className="inline-flex items-center">
          <Link to="/dashboard" className="hover:text-ui-text-primary transition-colors">
            Workspace
          </Link>
        </li>
        {pathnames.map((value, index) => {
          const to = `/${pathnames.slice(0, index + 1).join('/')}`;
          const isLast = index === pathnames.length - 1;
          const name = value.charAt(0).toUpperCase() + value.slice(1).replace('-', ' ');

          return (
            <li key={to} className="flex items-center">
              <span className="mx-2 text-ui-border">/</span>
              {isLast ? (
                <span className="text-ui-text-primary font-bold">{name}</span>
              ) : (
                <Link to={to} className="hover:text-ui-text-primary transition-colors">
                  {name}
                </Link>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
};

export default Breadcrumb;
