import 'reflect-metadata'
import app from "./app"
import { AppDataSource } from './db'

async function main () {
    try {
        await AppDataSource.initialize()
        app.listen(process.env.APP_PORT)
        console.log('Server listening on port', process.env.APP_PORT)
    } catch (e) {
        console.error("Error Catched: ", e)
    }
}

main()
