
import express from 'express';
import {Request,Response} from 'express';
import {vd,nd} from '../models/newdamages';


const newdamage = new nd();

const create = async (req:Request,res:Response) => {
    try {
   const newVehicle:vd = {
    vehicle_lisence:req.body.l,
    damage_id:req.body.d 

}

const adddamage= await newdamage.create(newVehicle);
res.status(200).json(adddamage);
    }
    catch(err){
res.status(500);
res.send(err);
    }
}

const damagesRoutes = (app:express.Application)=>{
app.post('/newdamage',create);
}