#include "mcc_generated_files/mcc.h"
#define carriageReturn  0x0D
#define nullChar        0x00
#define period          0x2E
#define EMC1001_ADDRESS 0x38   // slave device address
#define TEMP_HI         0       // EMC1001- temperature value high byte 
#define TEMP_LO         2       // EMC1001- low byte containing 1/4 deg fraction

void LEDsON(void)
{
    LED1_SetHigh();
    LED2_SetHigh();
    LED3_SetHigh();
    LED4_SetHigh();
}

void LEDsOFF(void)
{
    LED1_SetLow();
    LED2_SetLow();
    LED3_SetLow();
    LED4_SetLow();
}

uint8_t EMC1001_Read(uint8_t reg, uint8_t *pData)
{
    I2C2_MESSAGE_STATUS status = I2C2_MESSAGE_PENDING;
    static I2C2_TRANSACTION_REQUEST_BLOCK trb[2];
    
    I2C2_MasterWriteTRBBuild(&trb[0], &reg, 1, EMC1001_ADDRESS);
    I2C2_MasterReadTRBBuild(&trb[1], pData, 1, EMC1001_ADDRESS);                
    I2C2_MasterTRBInsert(2, &trb[0], &status);
    
    while(status == I2C2_MESSAGE_PENDING);      // blocking

    return (status == I2C2_MESSAGE_COMPLETE); 
} 

void main(void)
{
    int8_t  temp;
    uint8_t data;
    uint8_t templo;
    uint8_t failcount = 0x00;
    uint16_t fullTemp = 0x0000;
    SYSTEM_Initialize();
    INTERRUPT_GlobalInterruptEnable();
    INTERRUPT_PeripheralInterruptEnable();
    LEDsON();
    while(!TMR4_HasOverflowOccured());
    LEDsOFF();//  start with all leds low

    while (1)
    {
        if (TMR4_HasOverflowOccured())
            //LED4_Toggle();  //  just an indicator that things are working
        
        if (PIR3bits.RCIF)  //  operates on 1 second interval
        {
            //LED3_Toggle();
            data = EUSART_Read();       // read the eusart every second regardless
            if (data == 'G' && T6TMR == 0x00)  //  0x47 = 'G'
            {
                TMR6_Start();
                //LED1_Toggle();

                if (EMC1001_Read(TEMP_HI, (uint8_t*)&temp)) 
                {
                    EMC1001_Read(TEMP_LO, &templo);     // get lsb 
                    templo = templo >> 6;                   
                    if (temp < 0) 
                        templo = 3-templo;    // complement to 1 if T negative
                    EUSART_Write('K'); //  k (0x4B) just because

                    EUSART_Write((uint8_t)temp);
                    EUSART_Write(templo*25);
                    EUSART_Write('L'); //  LL as stop bit
                }
                TMR6_Stop();
            }
        }
    }
}