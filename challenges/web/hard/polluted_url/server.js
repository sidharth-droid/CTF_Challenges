const express = require('express');
const app = express();
const port = 3000;

app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  console.log('Headers:', req.headers);
  console.log('Query:', req.query);
  next();
});

app.get('/api/v1/info', (req, res) => {
  res.json({
    message: 'Welcome to the Discount API v1!',
    debug: 'For support, contact us with token=secret123'
  });
});

app.get('/api/v1/discount', (req, res) => {
  try {
    const roles = Array.isArray(req.query.role) ? req.query.role : [req.query.role || 'guest'];
    const token = req.query.token || '';
    const apiVersion = req.headers['x-api-version'] || '';

    if (apiVersion !== 'v1') {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Invalid API version. Please use X-API-Version: v1'
      });
    }

    if (token !== 'secret123') {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'Invalid token. Authentication required.'
      });
    }

    const firstRole = roles[0]; 
    const effectiveRole = roles[roles.length - 1]; 

    if (typeof firstRole !== 'string' || typeof effectiveRole !== 'string') {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Role must be a valid string.'
      });
    }

    if (!firstRole || !/admin/i.test(firstRole)) {
      if (effectiveRole === 'admin') {
        return res.status(200).json({
          discount_code: 'FLAG{P0llut3d_Adm1n}',
          message: 'Admin discount unlocked! Enjoy your exclusive offer.'
        });
      }
      return res.status(403).json({
        message: 'Access denied. Insufficient privileges.'
      });
    }

    return res.status(403).json({
      message: 'Access denied. Role validation failed.'
    });
  } catch (error) {
    console.error('Error:', error.message);
    return res.status(500).json({
      error: 'Internal Server Error',
      message: 'Something went wrong. Try again later.'
    });
  }
});

// Handle 404 for undefined routes
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: 'Endpoint not found. Check the API documentation.'
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Discount API server running on http://localhost:${port}`);
  console.log('CTF Challenge: Polluted Pathways: Admin Overload is live!');
});