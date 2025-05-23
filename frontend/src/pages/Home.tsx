import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Container,
  Typography,
  Button,
  Grid,
  Paper,
  Box,
} from '@mui/material';
import DescriptionIcon from '@mui/icons-material/Description';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ChatIcon from '@mui/icons-material/Chat';

const Home: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 8, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Welcome to Unemployment Claims
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Your trusted partner in managing unemployment benefits
        </Typography>
      </Box>

      <Grid container spacing={4} justifyContent="center">
        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              height: '100%',
            }}
          >
            <DescriptionIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h5" component="h2" gutterBottom>
              File a Claim
            </Typography>
            <Typography paragraph>
              Submit your unemployment claim quickly and easily through our streamlined process.
            </Typography>
            <Button
              component={RouterLink}
              to="/claim"
              variant="contained"
              color="primary"
              size="large"
              fullWidth
            >
              File Claim
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              height: '100%',
            }}
          >
            <DashboardIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h5" component="h2" gutterBottom>
              View Dashboard
            </Typography>
            <Typography paragraph>
              Track your claim status and view your benefits information in one place.
            </Typography>
            <Button
              component={RouterLink}
              to="/dashboard"
              variant="contained"
              color="primary"
              size="large"
              fullWidth
            >
              View Dashboard
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              height: '100%',
            }}
          >
            <ChatIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h5" component="h2" gutterBottom>
              Chat with Joy
            </Typography>
            <Typography paragraph>
              Get instant answers to your questions about unemployment benefits.
            </Typography>
            <Button
              component={RouterLink}
              to="/chat"
              variant="contained"
              color="primary"
              size="large"
              fullWidth
            >
              Start Chat
            </Button>
          </Paper>
        </Grid>
      </Grid>

      <Box sx={{ mt: 8, mb: 4 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Why Choose Us?
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom>
              Easy to Use
            </Typography>
            <Typography>
              Our intuitive interface makes filing claims and managing benefits simple.
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom>
              Fast Processing
            </Typography>
            <Typography>
              Get quick responses and updates on your claim status.
            </Typography>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom>
              24/7 Support
            </Typography>
            <Typography>
              Chat with Joy anytime for instant assistance with your questions.
            </Typography>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Home; 