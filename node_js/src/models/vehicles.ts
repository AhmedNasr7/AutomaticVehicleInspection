import client from '../database';




export type vehicle = {
   
    image:string;
    name:string;
    model:number;
    driver_name:string;
    license_number:String;
}

export class vehicles {

    async create(v:vehicle):Promise<vehicle> {
        try {
            const conn = await client.connect();
            const sql = 'INSERT INTO vehicles (image,name,model,driver_name,license_number) VALUES ($1,$2,$3,$4,$5) RETURNING *';
            const result = await conn.query(sql,[v.image,v.name,v.model,v.driver_name,v.license_number]);
             conn.release();
            return result.rows[0];
        }
        catch(err){
            throw new Error(`couldn't create vehicles, Error:${err}`);
        }
    }

    async index():Promise<vehicle[]> {
        try {
            const conn = await client.connect();
            const sql = 'SELECT * from vehicles';
            const result = await conn.query(sql)
             conn.release();
            return result.rows;
        }
        catch(err){
            throw new Error(`couldn't get vehicles, Error:${err}`);
        }
    }

    async show(id:string):Promise<vehicle>{
        try {
            const conn = await client.connect();
            const sql = 'SELECT * from vehicles where id = ($1)';
            const result = await conn.query(sql,[id]);
             conn.release();
            return result.rows[0];
        }
        catch(err){
            throw new Error(`couldn't get vehicles, Error:${err}`);
        }

    }

}