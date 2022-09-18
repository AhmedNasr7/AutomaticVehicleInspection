import express from 'express';
import {Request,Response} from 'express';
import {vehicle,vehicles} from '../models/vehicles';

const thevehicles = new vehicles();

const index = async (req:Request,res:Response)=>{
    const allvehicles = await thevehicles.index();
    res.json(allvehicles);
}

const create = async (req:Request,res:Response) => {
    try {
   const newVehicle:vehicle = {
    image:req.body.image,
    name:req.body.name,
    model:req.body.model,
    driver_name:req.body.drname,
    license_number:req.body.ln
   }
   const addvehicle = await thevehicles.create(newVehicle);
   res.status(200).json(addvehicle);
    }
    catch(err){
res.status(500);
res.send(err);
    }
}
const show = async (req:Request,res:Response)=> {
    try {
const targetvehicle = await thevehicles.show(req.params.id);
res.json(targetvehicle);
    }
    catch(err){
        res.status(400).json(err);

    }
}


const vehicleRoutes = (app:express.Application)=>{
    app.get('/vehicles',index);
    app.get('/vehicles/:id',show);
    app.post('/vehicles',create);
}

export default vehicleRoutes;