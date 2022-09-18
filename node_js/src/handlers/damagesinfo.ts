import express from 'express';
import {Request,Response} from 'express';
import {damageinfo,damagesdetails} from '../models/damagesinfo';


const damagesinfo = new damagesdetails();

const index = async (req:Request,res:Response)=>{
    const  damagesdet = await damagesinfo.index();
    res.json(damagesdet);
}

const create = async (req:Request,res:Response)=>{
    try{
   const newdamagetype:damageinfo = {
damage_name:req.body.dn,
damage_cost:req.body.dc,
healthy:req.body.healthy
   }
const adddamage = await damagesinfo.create(newdamagetype);
res.status(200).json(adddamage);
    }
    catch(err){
        res.status(500);
        res.send(err);
    }
}


const newdamageRoutes = (app:express.Application)=>{
    app.get('/damagesinfo',index);
    app.post('/damagesinfo',create);
}

export default newdamageRoutes;