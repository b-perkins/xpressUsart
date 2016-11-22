#include "mcc_generated_files/mcc.h"
#define carriageReturn 0x0D
#define nullChar    0x00
bool toggle = true;
void main(void)
{
    SYSTEM_Initialize();
    //INTERRUPT_GlobalInterruptEnable();
    //INTERRUPT_PeripheralInterruptEnable();

    while (1)
    {
        if (TMR6_HasOverflowOccured())
        {
            LED1_Toggle();
            if (toggle)
            {
                EUSART_Write(0x41); //A
                EUSART_Write(0x42); //B
                EUSART_Write(carriageReturn);
                toggle = false;
            }
            else
            {
                EUSART_Write(0x46); //F
                EUSART_Write(0x47); //G
                EUSART_Write(carriageReturn);
                toggle = true;
            }

        }
    }
}