import client from '../database';

export type damageinfo = {
    damage_name:string;
    damage_cost:number;
    healthy:number;
}

export class  damagesdetails{


async create(d:damageinfo):Promise<damageinfo>{
    try {
const conn  =  await client.connect()
const sql = 'INSERT INTO damagesinfo (damage_name,damage_cost,healthy) VALUES ($1,$2,$3) RETURNING *';
const result =  await conn.query(sql,[d.damage_name,d.damage_cost,d.healthy]);
conn.release()
return result.rows[0];

}
    catch(err){
        throw new Error(`couldn't create vehicles, Error:${err}`);
    }
}

async index():Promise<damageinfo[]>{
    try{
const conn = await client.connect();
const sql = 'select * from damagesinfo';
const result = await conn.query(sql);
conn.release()
return result.rows;
    }
    catch(err){
        throw new Error(`couldn't get vehicles, Error:${err}`);
    }
}
}