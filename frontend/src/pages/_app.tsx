import { AppProps } from 'next/app';

import { AuthProvider } from '@/contexts/AuthContext';
import Layout from '@/components/Layout';
import '@/styles/globals.css';

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </AuthProvider>
  );
}