import React from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';

// Mock data - replace with actual API call
const mockClaims = [
  {
    id: 1,
    date: '2023-11-01',
    status: 'approved',
    employer: 'Tech Corp',
    fraudScore: 0.1,
  },
  {
    id: 2,
    date: '2023-10-15',
    status: 'denied',
    employer: 'Old Company',
    fraudScore: 0.8,
  },
];

const Dashboard = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Claims Dashboard
        </Typography>

        <TableContainer component={Paper} sx={{ mt: 4 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Employer</TableCell>
                <TableCell>Fraud Score</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {mockClaims.map((claim) => (
                <TableRow key={claim.id}>
                  <TableCell>{claim.date}</TableCell>
                  <TableCell>
                    <Typography
                      color={claim.status === 'approved' ? 'success.main' : 'error.main'}
                    >
                      {claim.status.toUpperCase()}
                    </Typography>
                  </TableCell>
                  <TableCell>{claim.employer}</TableCell>
                  <TableCell>{claim.fraudScore}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Container>
  );
};

export default Dashboard; 