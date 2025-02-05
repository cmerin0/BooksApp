import { DataSource } from 'typeorm';
import { Book } from './entities/Book';

console.log(process.env.DB_PORT)

export const AppDataSource = new DataSource({
    type: 'postgres',
    host: process.env.DB_HOST,
    username: process.env.DB_USER,
    password: process.env.DB_PASS,
    port: parseInt(process.env.DB_PORT || '5432', 10),
    database: process.env.DB_NAME,
    entities: [Book],
    logging: true,
    synchronize: false
});