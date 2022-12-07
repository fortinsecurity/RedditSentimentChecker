import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import './App.css';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Container from '@mui/material/Container';
import GitHubIcon from '@mui/icons-material/GitHub';
import FacebookIcon from '@mui/icons-material/Facebook';
import TwitterIcon from '@mui/icons-material/Twitter';
import LinkedinIcon from '@mui/icons-material/LinkedIn';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Header from './Header';
import MainFeaturedPost from './MainFeaturedPost';
import FeaturedPost from './FeaturedPost';
import Main from './Main';
import Sidebar from './Sidebar';
import Footer from './Footer';
import post1 from './blog-post.1.md';
import post2 from './blog-post.2.md';
import post3 from './blog-post.3.md';

const sections = [
  { title: 'Technology', url: '#' },
  { title: 'Design', url: '#' },
  { title: 'Culture', url: '#' },
  { title: 'Business', url: '#' },
  { title: 'Politics', url: '#' },
  { title: 'Opinion', url: '#' },
  { title: 'Science', url: '#' },
  { title: 'Health', url: '#' },
  { title: 'Style', url: '#' },
  { title: 'Travel', url: '#' },
];

const mainFeaturedPost = {
  title: 'Title of a longer featured blog post',
  description:
    "Multiple lines of text that form the lede, informing new readers quickly and efficiently about what's most interesting in this post's contents.",
  image: 'https://source.unsplash.com/random',
  imageText: 'main image description',
  linkText: 'Continue reading…',
};

const featuredPosts = [
  {
    title: 'Featured post',
    date: 'Nov 12',
    description:
      'This is a wider card with supporting text below as a natural lead-in to additional content.',
    image: 'https://source.unsplash.com/random',
    imageLabel: 'Image Text',
  },
  {
    title: 'Post title',
    date: 'Nov 11',
    description:
      'This is a wider card with supporting text below as a natural lead-in to additional content.',
    image: 'https://source.unsplash.com/random',
    imageLabel: 'Image Text',
  },
];

const posts = [post1, post2, post3];
const results = {"subreddit": "cryptocurrency", "topic": "ethereum", "sentiment": "0.4"}

const sidebar = {
  title: 'About',
  description:
    'Want to subscribe to a new topic? Login first, then the "Subscribe" button for a query of your liking.',
  archives: [
    { title: 'cryptocurrency # bitcoin', url: '#' },
    { title: 'OutOfTheLoop # musk', url: '#' },
    { title: 'metaverse # facebook', url: '#' },
  ],
  social: [
    { name: 'LinkedIn', icon: LinkedinIcon },
    { name: 'GitHub', icon: GitHubIcon },
    { name: 'Twitter', icon: TwitterIcon },
    { name: 'Facebook', icon: FacebookIcon }
  ],
  footer:  "Just some test web app. Copyright © 2022"
};

const theme = createTheme();

export default function Blog() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Header title="Blog" sections={sections} />
        <main>
          <MainFeaturedPost post={mainFeaturedPost} />
          <Grid container spacing={5} sx={{ mt: 3 }}>
            <Main title="Sentiment Crawler" posts={posts} results={results} />
            <Sidebar
              title={sidebar.title}
              description={sidebar.description}
              archives={sidebar.archives}
              social={sidebar.social}
              footer={sidebar.footer}
            />
          </Grid>
        </main>
      </Container>
    </ThemeProvider>
  );
}

// original

{/* <ThemeProvider theme={theme}>
<CssBaseline />
<Container maxWidth="lg">
  <Header title="Blog" sections={sections} />
  <main>
    <MainFeaturedPost post={mainFeaturedPost} />
    <Grid container spacing={4}>
      {featuredPosts.map((post) => (
        <FeaturedPost key={post.title} post={post} />
      ))}
    </Grid>
    <Grid container spacing={5} sx={{ mt: 3 }}>
      <Main title="From the firehose" posts={posts} />
      <Sidebar
        title={sidebar.title}
        description={sidebar.description}
        archives={sidebar.archives}
        social={sidebar.social}
      />
    </Grid>
  </main>
</Container>
<Footer
  title="Footer"
  description="Something here to give the footer a purpose!"
/>
</ThemeProvider> */}