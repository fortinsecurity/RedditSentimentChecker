import * as React from 'react';
import { useState } from 'react';
import PropTypes from 'prop-types';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import Markdown from './Markdown';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import TextField from '@mui/material/TextField';

function Main(props) {
  /* var { posts, title,results } = props; */
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [results, setResults] = useState(props["results"]);
  const posts = props["posts"];
  const title = props["title"];

 
  const jsonParsedResults = results // JSON.parse(results)
//   this.state = {
//     results: {
//         subreddit: "testsubreddit",
//         topic:"testtopic",
//         sentiment:"testsentiment"
//     }
//   }
  const resultsFormatted = "Crawled " +jsonParsedResults["subreddit"]+ " for topic "+jsonParsedResults["topic"] +".\n The sentiment on this topic is: " +jsonParsedResults["sentiment"] +" (on a scale from -1 to 1)."
  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log({subreddit: data.get('subreddit')
    });
    fetch("http://localhost:8000/sentiment?subreddit="+data.get('subreddit')+"&topic="+data.get('topic')+"&limit=2")
      .then(res => res.json())
      .then(
        (result) => {
          console.log(result)
          setIsLoaded(true);
          setResults(result);
        //   results = result

        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
            console.log(error)
            setIsLoaded(true);
            setError(error);
        }
      )
  };


  // old

/*   function Main(props) {
    const { posts, title,results } = props;
    const jsonParsedResults = results // JSON.parse(results)
    const resultsFormatted = "Crawled " +jsonParsedResults["subreddit"]+ " for topic "+jsonParsedResults["topic"] +".\n The sentiment on this topic is: " +jsonParsedResults["sentiment"] +" (on a scale from -1 to 1)."
    const handleSubmit = (event) => {
      event.preventDefault();
      const data = new FormData(event.currentTarget);
      console.log({
        email: data.get('email'),
        password: data.get('password'),
      });
      res = 
    };
   */


  return (
    <Grid
      item
      xs={12}
      md={8}
      sx={{
        '& .markdown': {
          py: 3,
        },
      }}
    >
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <Divider />
      <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Subreddit"
              name="subreddit"
              autoComplete=""
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="topic"
              label="Topic"
              type="topic"
              id="topic"
              autoComplete=""
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Submit
            </Button>
        </Box>
        <Typography variant="h6" gutterBottom sx={{ "margin-top":"3em" }}>
        Results
      </Typography>
      <Divider />
      <Box sx={{ mt: 1 }}>
        <Paper elevation={3} sx={{height: "40%", padding: "1em", "margin-top":"1em"}}>
            {!results &&
                <span style={{color:"lightgray"}}>Your results will be visible here.</span>
            }
            {results &&
                <p>Crawled {results["subreddit"]} for topic {results["topic"]}.</p>
            }
            {results &&
                <p>The sentiment on this topic is: {parseFloat(results["sentiment"]).toFixed(2)} (on a scale from -1 to 1).</p>
            }
            </Paper>
        </Box>
    </Grid>
  );
}

Main.propTypes = {
  posts: PropTypes.arrayOf(PropTypes.string).isRequired,
  title: PropTypes.string.isRequired,
};

export default Main;

// original: after button

{/* <Grid container>
              <Grid item xs>
                <Link href="#" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item>
                <Link href="#" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>

 */}