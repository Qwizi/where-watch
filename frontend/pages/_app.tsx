import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap'
import Head from 'next/head'
function MyApp({ Component, pageProps }: AppProps) {

  return (
    <div>
      <Head>
      <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
        integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3"
        crossOrigin="anonymous"
      />
      </Head>
      <Navbar bg="dark" expand="lg" variant="dark">
        <Container>
          <Navbar.Brand href="/">GdzieObejrze.tk</Navbar.Brand>
        </Container>
      </Navbar>
      <Container>
        <Component {...pageProps} />
    </Container>
    </div>
  )
}

export default MyApp
