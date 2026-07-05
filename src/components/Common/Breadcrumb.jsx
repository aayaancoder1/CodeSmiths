import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const Breadcrumb = ({ className = '' }) => {
  const location = useLocation();
  const pathnames = location.pathname.split('/').filter((x) => x);

  return (
    <nav aria-label="breadcrumb" className={`flex items-center text-xs font-medium text-slate-400 ${className}`}>
      <ol className="inline-flex items-center space-x-1 md:space-x-2">
        <li className="inline-flex items-center">
          <Link to="/dashboard" className="hover:text-slate-200 transition-colors">
            Home
          </Link>
        </li>
        {pathnames.map((value, index) => {
          const to = `/${pathnames.slice(0, index + 1).join('/')}`;
          const isLast = index === pathnames.length - 1;
          const name = value.charAt(0).toUpperCase() + value.slice(1).replace('-', ' ');

          return (
            <li key={to} className="flex items-center">
              <span className="mx-2 text-slate-600 font-normal">/</span>
              {isLast ? (
                <span className="text-slate-200 font-semibold">{name}</span>
              ) : (
                <Link to={to} className="hover:text-slate-200 transition-colors">
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
