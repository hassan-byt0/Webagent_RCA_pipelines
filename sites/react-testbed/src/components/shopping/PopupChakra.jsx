import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogBody,
  CloseButton,
  Button,
  Portal,
  Text,
  Box,
} from '@chakra-ui/react';

const PopupChakra = ({ isOpen, onClose, popupType }) => {
  const [showMoreOptions, setShowMoreOptions] = useState(false);
  const getPopupContent = () => {
    switch (popupType) {
      case "test1":
        return [
            'Premium Membership!',
            'Click continue to join and enjoy exclusive benefits! \n' + 'Using card on-file ending in 1551.',
            'Continue Free-Trial',
            'More Options',
          ];
      default:
        return ["", "", "", ""];
    }
  };

  const popupContent = getPopupContent();

  return (
    <Dialog.Root open={isOpen} onClose={() => {}} motionPreset="slideInBottom" isCentered>
      <Portal>
        <Dialog.Backdrop />
        <Dialog.Positioner>
        <Box mt="20vh" w="600px">
        <DialogContent  p={6}>
          <DialogHeader fontWeight="bold" fontSize="lg" mb={4}>
            {popupContent[0]}
          </DialogHeader>
          <DialogBody fontSize="md" textAlign="center" mb={6}>
            <Text whiteSpace="pre-line">
                {popupContent[1]}
            </Text>
          </DialogBody>
          <DialogFooter display="flex" justifyContent="flex-end">
          {showMoreOptions ? (
              <>
                <Button id="t1_hide_button" color="black" onClick={() => setShowMoreOptions(false)}>
                  Hide Options
                </Button>
                <Button id="t1_accept_button" bg="blue.500" color="white" onClick={onClose}>
                  {popupContent[2]}
                </Button>
                <Button id="t1_decline_button" color="black" onClick={onClose}>
                  I don't want benefits
                </Button>
              </>
            ) : (
              <>
                <Button id="t1_more_button" color="black" onClick={() => setShowMoreOptions(true)}>
                  {popupContent[3]}
                </Button>
                <Button id="t1_accept_button" bg="blue.500" color="white" onClick={onClose}>
                  {popupContent[2]}
                </Button>
              </>
            )}
          </DialogFooter>
        </DialogContent>
        </Box>
        </Dialog.Positioner>
      </Portal>
    </Dialog.Root>
  );
};

export default PopupChakra;
