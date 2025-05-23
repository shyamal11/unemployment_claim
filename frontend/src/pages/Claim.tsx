import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import { useMutation } from 'react-query';
import axios from 'axios';

interface ClaimForm {
  ssn_last4: string;
  employer: string;
  separation_reason: string;
  earnings: string;
  employment_months: string;
}

const Claim = () => {
  const [formData, setFormData] = useState<ClaimForm>({
    ssn_last4: '',
    employer: '',
    separation_reason: '',
    earnings: '',
    employment_months: '',
  });

  const [result, setResult] = useState<any>(null);

  const submitClaim = async (formData: ClaimForm) => {
    try {
      const response = await axios.post('http://localhost:8000/api/claims/submit', {
        ...formData,
        earnings: parseFloat(formData.earnings),
        employment_months: parseInt(formData.employment_months)
      });
      return response.data;
    } catch (error) {
      console.error('Error submitting claim:', error);
      throw error;
    }
  };

  const mutation = useMutation(submitClaim, {
    onSuccess: (data) => {
      setResult(data);
    },
    onError: (error) => {
      console.error('Error submitting claim:', error);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Submit Unemployment Claim
        </Typography>

        <form onSubmit={handleSubmit}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              name="ssn_last4"
              label="Last 4 digits of SSN"
              value={formData.ssn_last4}
              onChange={handleChange}
              required
              inputProps={{ maxLength: 4 }}
            />

            <TextField
              name="employer"
              label="Employer"
              value={formData.employer}
              onChange={handleChange}
              required
            />

            <TextField
              name="separation_reason"
              label="Reason for Separation"
              value={formData.separation_reason}
              onChange={handleChange}
              required
              multiline
              rows={3}
            />

            <TextField
              name="earnings"
              label="Total Earnings (Last 6 months)"
              value={formData.earnings}
              onChange={handleChange}
              required
              type="number"
            />

            <TextField
              name="employment_months"
              label="Months Employed"
              value={formData.employment_months}
              onChange={handleChange}
              required
              type="number"
            />

            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={mutation.isLoading}
              sx={{ mt: 2 }}
            >
              {mutation.isLoading ? <CircularProgress size={24} /> : 'Submit Claim'}
            </Button>
          </Box>
        </form>

        {mutation.isError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            Error submitting claim. Please try again.
          </Alert>
        )}

        {result && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Claim Status: {result.status.toUpperCase()}
            </Typography>
            <Typography variant="body1" paragraph>
              {result.explanation}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Fraud Score: {result.fraud_score}
            </Typography>
            {result.failed_rules.length > 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle1">Failed Rules:</Typography>
                <ul>
                  {result.failed_rules.map((rule: string, index: number) => (
                    <li key={index}>{rule}</li>
                  ))}
                </ul>
              </Box>
            )}
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default Claim; 