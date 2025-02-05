import { Entity, PrimaryGeneratedColumn, Column, BaseEntity, CreateDateColumn, UpdateDateColumn } from 'typeorm'

@Entity("books")
export class Book extends BaseEntity{
    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    title: string;

    @Column()
    author: string;

    @Column()
    description: string;

    @Column()
    cover_url: string;

    @Column()
    availability: boolean;

    @CreateDateColumn({ type: 'timestamp', default: () => 'NOW()'})
    created_at: Date;

    @UpdateDateColumn()
    updated_at: Date;

}