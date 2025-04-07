import React from 'react';
import '../styles/globals.css'; // Make sure this path matches your CSS file

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}