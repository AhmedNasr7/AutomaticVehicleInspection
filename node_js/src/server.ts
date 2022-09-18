const express = require('express');
import multer from 'multer';
import dotenv from 'dotenv';
import vehicleRoutes from './handlers/vehicles';
import newdamageRoutes from './handlers/damagesinfo';
import userRoute from './handlers/userdata';
const app = express()
const port = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());


vehicleRoutes(app);
newdamageRoutes(app);
userRoute(app);

app.listen(port,()=>{
console.log(`app is listening on port ${port}`)
})

export default app;