import express from 'express'
import morgan from 'morgan'
import cors from 'cors'
import dotenv from 'dotenv';
import bookRoutes from './routes/book.routes'

dotenv.config(); // Load environment variables

const app = express() // Initialize the app

app.use(morgan('dev'))
app.use(cors())
app.use(express.json())

app.use(bookRoutes)

export default app