

import client from '../database';

export type vd = {
    vehicle_lisence:string;
    damage_id:String;
}

export class nd {

    async create(v:vd):Promise<vd> {
        try {
            const conn = await client.connect();
            const sql = 'INSERT INTO vehicles (vehicle_license,damage_id) VALUES ($1,$2) RETURNING *';
            const result = await conn.query(sql,[v.vehicle_lisence,v.damage_id]);
             conn.release();
            return result.rows[0];
        }
        catch(err){
            throw new Error(`couldn't create vehicles, Error:${err}`);
        }
    }

}
