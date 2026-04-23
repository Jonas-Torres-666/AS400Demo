**free
ctl-opt main(main) actgrp(*caller);

/copy qrpglesrc/jiratasks.rpgle

dcl-proc main;
   
  snd-msg 'Hello, World! this is task 1';
  
  printJiraTasks();
    
end-proc;
 