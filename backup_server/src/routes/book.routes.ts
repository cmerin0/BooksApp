import { Router } from "express";
import { getBooks, getBook, createBook, updateBook, deleteBook } from "../controllers/book.controller"

const router = Router()

// Beginning of routes 
router.get('/api/books', getBooks)
router.get('/api/books/:id', getBook)
router.post('/api/books', createBook)
router.put('/api/books/:id', updateBook)
router.delete('/api/books/:id', deleteBook)

export default router