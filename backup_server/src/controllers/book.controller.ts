import { Request, Response } from "express";
import { Book } from "../entities/Book"

export const getBooks = async (req: Request, res: Response) => {
    try {
        const books = await Book.find()
        res.status(201).json({'data': books, 'source': 'database backup'})
        return
    } catch (e) {
        if (e instanceof Error)
            res.status(500).json({"Error": "An Error occurred while fetching books", message: e.message })
        return
    }
}

export const getBook = async (req: Request, res: Response) => {

    const { id }= req.params

    try {
        const book = await Book.findOneBy(({ id: parseInt(id)}))

        if (!book) {
            res.status(404).json({'message': 'Book not found'})
            return
        }
        res.status(201).json({'data': book, 'source': 'database backup'})
        return

    } catch (e) {
        if (e instanceof Error)
            res.status(500).json({"Error": "An Error occurred while fetching a book", message: e.message})
        return
    }
}

export const createBook = async (req: Request, res: Response) => {
    try {
        const { title, author, description, cover_url, availability } = req.body
        const book = new Book()
        book.title = title
        book.author = author
        book.description = description
        book.cover_url = cover_url
        book.availability = availability

        await book.save()

        res.status(201).json({ 'message': 'Book Created Successully' })
        return 
        
    } catch (e) {
        if (e instanceof Error)
            res.status(500).json({"Error": "An Error occurred while creating a book", message: e.message})
        return
    }

}

export const updateBook = async (req: Request, res: Response) => {
    
    const { id }= req.params
    
    try {
        const book = await Book.findOneBy(({ id: parseInt(id)}))

        if (!book) {
            res.status(404).json({ message: "Book not Found"})
            return
        }

        await Book.update({ id: parseInt(id)}, req.body) // Proceeding to update book if exists

        res.status(201).json({ 'message': 'Book Updated Successully' }) // Returns 204 Updated successfully!
        return

    } catch (e) {
        if (e instanceof Error)
            res.status(500).json({"Error": "An Error occurred while updating a book", message: e.message})
        return
    }
}

export const deleteBook = async (req: Request, res: Response) => {
    
    const { id }= req.params
    
    try {
        const deleted_book = await Book.delete(({ id: parseInt(id)}))

        if (deleted_book.affected === 0) {
            res.status(404).json({ 'message': 'Book not found'})
            return
        }

        res.status(201).json({ 'message': 'Book Deleted Successfully', 'ID': id }) // Returns 204 Updated successfully!
        return

    } catch (e) {
        if (e instanceof Error)
            res.status(500).json({"Error": "An Error occurred while deleting a book", message: e.message})
        return
    }
}