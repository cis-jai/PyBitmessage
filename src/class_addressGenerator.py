"""
A thread for creating addresses
"""
import hashlib
import time
from binascii import hexlify
import threading
try:
    import defaults
    import highlevelcrypto
    import queues
    import shared
    import state
    import tr
    from addresses import decodeAddress, encodeAddress, encodeVarint
    from bmconfigparser import BMConfigParser
    from fallback import RIPEMD160Hash
    from pyelliptic import arithmetic
    from pyelliptic.openssl import OpenSSL
    from network.threads import StoppableThread
    from debug import logger 
except ModuleNotFoundError:
    from pybitmessage import defaults
    from pybitmessage.debug import logger 
    from pybitmessage import highlevelcrypto
    from pybitmessage import queues
    from pybitmessage import shared
    from pybitmessage import state
    from pybitmessage import tr
    from pybitmessage.addresses import decodeAddress, encodeAddress, encodeVarint
    from pybitmessage.bmconfigparser import BMConfigParser
    from pybitmessage.fallback import RIPEMD160Hash
    from pybitmessage.pyelliptic import arithmetic
    from pybitmessage.pyelliptic.openssl import OpenSSL
    from pybitmessage.network.threads import StoppableThread

class addressGenerator(StoppableThread):
    """A thread for creating addresses"""
    name = "addressGenerator"

    def __init__(self):
        StoppableThread.__init__(self)
        self.lock = threading.Lock()
    
    def stopThread(self):
        try:
            queues.addressGeneratorQueue.put(("stopThread", "data"))
        except:
            pass
        super(addressGenerator, self).stopThread()

    def run(self):
        """
        Process the requests for addresses generation
        from `.queues.addressGeneratorQueue`
        """
        logger.error('addressGenerator addressGenerator')
        logger.error('state.shutdown-{}'.format(state.shutdown))
        logger.error('--------self----{}'.format(self))
        while state.shutdown == 0:
            logger.error(
                    'qqqqqqqqq1111111111111111111111111111111')
            try:
                queueValue = queues.addressGeneratorQueue.get()
                logger.error('SuccessFully Loaded')
            except Exception as e:
                import traceback
                logger.error('Traceback-{} \n'.format(
                    str(traceback.format_stack())))
                logger.error('Address Genertor excepation 7777')
                logger.error(e)
            nonceTrialsPerByte = 0
            # logger.error('$$$$$$$$$$$$ queueValue  @@@@@@@@@@@-{}'.format(queueValue))
            payloadLengthExtraBytes = 0
            live = True
            logger.error(
                    'qqqqqqqqq3333333333333333333333333333333')
            logger.error(
                    'qqqqqqqqq33333333333333-{}'.format(queueValue[0] ))
            if queueValue[0] == 'createChan':
                logger.error(
                    'OOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
                command, addressVersionNumber, streamNumber, label, \
                    deterministicPassphrase, live = queueValue
                logger.error('++++++++++++100++++++++++++')
                eighteenByteRipe = False
                logger.error('++++++++++++102++++++++++++')
                numberOfAddressesToMake = 1
                logger.error('++++++++++++104++++++++++++')
                numberOfNullBytesDemandedOnFrontOfRipeHash = 1
            elif queueValue[0] == 'joinChan':
                logger.info(
                    '111111111111111111111111111111111111111')
                command, chanAddress, label, deterministicPassphrase, \
                    live = queueValue
                eighteenByteRipe = False
                addressVersionNumber = decodeAddress(chanAddress)[1]
                streamNumber = decodeAddress(chanAddress)[2]
                numberOfAddressesToMake = 1
                numberOfNullBytesDemandedOnFrontOfRipeHash = 1
            elif len(queueValue) == 7:
                logger.info(
                    '22222222222222222222222222222222222222')
                command, addressVersionNumber, streamNumber, label, \
                    numberOfAddressesToMake, deterministicPassphrase, \
                    eighteenByteRipe = queueValue
                try:
                    numberOfNullBytesDemandedOnFrontOfRipeHash = \
                        BMConfigParser().getint(
                            'bitmessagesettings',
                            'numberofnullbytesonaddress'
                        )
                except:
                    if eighteenByteRipe:
                        numberOfNullBytesDemandedOnFrontOfRipeHash = 2
                    else:
                        # the default
                        numberOfNullBytesDemandedOnFrontOfRipeHash = 1
            elif len(queueValue) == 9:
                
                logger.error('createRandomAddress 122')
                command, addressVersionNumber, streamNumber, label, \
                    numberOfAddressesToMake, deterministicPassphrase, \
                    eighteenByteRipe, nonceTrialsPerByte, \
                    payloadLengthExtraBytes = queueValue
                logger.error('createRandomAddress 126')
                try:
                    logger.error('createRandomAddress 128')
                    numberOfNullBytesDemandedOnFrontOfRipeHash = \
                        BMConfigParser().getint(
                            'bitmessagesettings',
                            'numberofnullbytesonaddress'
                        )
                    logger.error('createRandomAddress 134')
                except:
                    logger.error('createRandomAddress 136')
                    if eighteenByteRipe:
                        logger.error('createRandomAddress 138')
                        numberOfNullBytesDemandedOnFrontOfRipeHash = 2
                    else:
                        logger.error('createRandomAddress 141')
                        # the default
                        numberOfNullBytesDemandedOnFrontOfRipeHash = 1
            elif queueValue[0] == 'stopThread':
                logger.info(
                    '444444444444444444444444444444444444444444')
                break
            else:
                logger.info(
                    'Programming error: A structure with the wrong number'
                    ' of values was passed into the addressGeneratorQueue.'
                    ' Here is the queueValue: %r\n', queueValue)
            logger.error('createRandomAddress 153')
            if addressVersionNumber < 3 or addressVersionNumber > 4:
                self.logger.error(
                    'Program error: For some reason the address generator'
                    ' queue has been given a request to create at least'
                    ' one version %s address which it cannot do.\n',
                    addressVersionNumber)
            logger.error('createRandomAddress 160')
            if nonceTrialsPerByte == 0:
                logger.error('++++++++++++170++++++++++++')
                nonceTrialsPerByte = BMConfigParser().getint(
                    'bitmessagesettings', 'defaultnoncetrialsperbyte')
            logger.error('createRandomAddress 165')
            try:
                if nonceTrialsPerByte < \
                        defaults.networkDefaultProofOfWorkNonceTrialsPerByte:
                    logger.error('++++++++++++175++++++++++++')
                    nonceTrialsPerByte = \
                        defaults.networkDefaultProofOfWorkNonceTrialsPerByte
            except Exception as e:
                logger.error('type(nonceTrialsPerByte) -{}'.format(
                    type(nonceTrialsPerByte)))
                logger.error('type(defaults.networkDefaultProofOfWorkNonceTrialsPerByte) -{}'.format(
                    type(defaults.networkDefaultProofOfWorkNonceTrialsPerByte)))
                logger.error('createRandomAddress except')
                logger.error(str(e))
            logger.error('createRandomAddress 171')
            if payloadLengthExtraBytes == 0:
                logger.error('++++++++++++179++++++++++++')
                payloadLengthExtraBytes = BMConfigParser().getint(
                    'bitmessagesettings', 'defaultpayloadlengthextrabytes')
            logger.error('createRandomAddress 176')
            if payloadLengthExtraBytes < \
                    defaults.networkDefaultPayloadLengthExtraBytes:
                logger.error('++++++++++++184++++++++++++')
                payloadLengthExtraBytes = \
                    defaults.networkDefaultPayloadLengthExtraBytes
            logger.error('createRandomAddress 181')
            if command == 'createRandomAddress':
                logger.error('++++++++++++188++++++++++++')
                queues.UISignalQueue.put((
                    'updateStatusBar', ""
                ))
                logger.error('&&&&&&&&&&&&&&&&&&&&&&&')
                logger.error('---------144--------------')
                logger.error('&&&&&&&&&&&&&&&&&&&&&&&')
                # This next section is a little bit strange. We're going
                # to generate keys over and over until we find one
                # that starts with either \x00 or \x00\x00. Then when
                # we pack them into a Bitmessage address, we won't store
                # the \x00 or \x00\x00 bytes thus making the address shorter.
                logger.error('createRandomAddress 190')
                startTime = time.time()
                numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix = 0
                logger.error('createRandomAddress 193')
                potentialPrivSigningKey = OpenSSL.rand(32)
                logger.error('createRandomAddress 194')
                potentialPubSigningKey = highlevelcrypto.pointMult(
                    potentialPrivSigningKey)
                logger.error('&&&&&&&&&&&&&&&&&&&&&&&')
                logger.error('---------157--------------')
                logger.error('&&&&&&&&&&&&&&&&&&&&&&&\n')
                while True:
                    numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix += 1
                    potentialPrivEncryptionKey = OpenSSL.rand(32)
                    potentialPubEncryptionKey = highlevelcrypto.pointMult(
                        potentialPrivEncryptionKey)
                    sha = hashlib.new('sha512')
                    sha.update(
                        potentialPubSigningKey + potentialPubEncryptionKey)
                    ripe = RIPEMD160Hash(sha.digest()).digest()
                    if (
                        ripe[:numberOfNullBytesDemandedOnFrontOfRipeHash] ==
                        '\x00'.encode('utf-8') * numberOfNullBytesDemandedOnFrontOfRipeHash
                    ):
                        break
                logger.error('&&&&&&&&&&&&&&&&&&&&&&&')
                logger.error('---------174--------------')
                logger.error('&&&&&&&&&&&&&&&&&&&&&&&\n')
                self.logger.error(
                    'Generated address with ripe digest: %s', hexlify(ripe))
                try:
                    self.logger.info(
                        'Address generator calculated %s addresses at %s'
                        ' addresses per second before finding one with'
                        ' the correct ripe-prefix.',
                        numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix,
                        numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix
                        / (time.time() - startTime))
                except ZeroDivisionError:
                    # The user must have a pretty fast computer.
                    # time.time() - startTime equaled zero.
                    pass
                logger.error('&&&&&&&&&&&&&&&&&&&&&&&')
                logger.error('---------191--------------')
                logger.error('&&&&&&&&&&&&&&&&&&&&&&&\n')
                address = encodeAddress(
                    addressVersionNumber, streamNumber, ripe)

                # An excellent way for us to store our keys
                # is in Wallet Import Format. Let us convert now.
                # https://en.bitcoin.it/wiki/Wallet_import_format
                privSigningKey = '\x80'.encode('raw_unicode_escape') + potentialPrivSigningKey
                checksum = hashlib.sha256(hashlib.sha256(
                    privSigningKey).digest()).digest()[0:4]
                privSigningKeyWIF = arithmetic.changebase(
                    privSigningKey + checksum, 256, 58)

                privEncryptionKey = '\x80'.encode('raw_unicode_escape') + potentialPrivEncryptionKey
                checksum = hashlib.sha256(hashlib.sha256(
                    privEncryptionKey).digest()).digest()[0:4]
                privEncryptionKeyWIF = arithmetic.changebase(
                    privEncryptionKey + checksum, 256, 58)
                BMConfigParser().add_section(address)
                BMConfigParser().set(address, 'label', label)
                BMConfigParser().set(address, 'enabled', 'true')
                BMConfigParser().set(address, 'decoy', 'false')
                BMConfigParser().set(address, 'noncetrialsperbyte', str(
                    nonceTrialsPerByte))
                BMConfigParser().set(address, 'payloadlengthextrabytes', str(
                    payloadLengthExtraBytes))
                BMConfigParser().set(
                    address, 'privsigningkey', privSigningKeyWIF)
                BMConfigParser().set(
                    address, 'privencryptionkey', privEncryptionKeyWIF)
                BMConfigParser().save()

                # The API and the join and create Chan functionality
                # both need information back from the address generator.
                queues.apiAddressGeneratorReturnQueue.put(address)
                queues.UISignalQueue.put((
                    'updateStatusBar', ""
                ))
                queues.UISignalQueue.put(('writeNewAddressToTable', (
                    label, address, streamNumber)))
                shared.reloadMyAddressHashes()
                if addressVersionNumber == 3:
                    queues.workerQueue.put((
                        'sendOutOrStoreMyV3Pubkey', ripe))
                elif addressVersionNumber == 4:
                    queues.workerQueue.put((
                        'sendOutOrStoreMyV4Pubkey', address))

            elif command == 'createPaymentAddress':
                queues.UISignalQueue.put((
                    'updateStatusBar', ""
                ))
                # This next section is a little bit strange. We're going
                # to generate keys over and over until we find one
                # that starts with either \x00 or \x00\x00. Then when
                # we pack them into a Bitmessage address, we won't store
                # the \x00 or \x00\x00 bytes thus making the address shorter.
                startTime = time.time()
                numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix = 0
                potentialPrivSigningKey = OpenSSL.rand(32)
                potentialPubSigningKey = highlevelcrypto.pointMult(
                    potentialPrivSigningKey)
                while True:
                    numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix += 1
                    potentialPrivEncryptionKey = OpenSSL.rand(32)
                    potentialPubEncryptionKey = highlevelcrypto.pointMult(
                        potentialPrivEncryptionKey)
                    sha = hashlib.new('sha512')
                    sha.update(
                        potentialPubSigningKey + potentialPubEncryptionKey)
                    ripe = RIPEMD160Hash(sha.digest()).digest()
                    if (
                        ripe[:numberOfNullBytesDemandedOnFrontOfRipeHash] ==
                        '\x00'.encode('utf-8') * numberOfNullBytesDemandedOnFrontOfRipeHash
                    ):
                        break
                self.logger.info(
                    'Generated address with ripe digest: %s', hexlify(ripe))
                try:
                    self.logger.info(
                        'Address generator calculated %s addresses at %s'
                        ' addresses per second before finding one with'
                        ' the correct ripe-prefix.',
                        numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix,
                        numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix
                        / (time.time() - startTime))
                except ZeroDivisionError:
                    # The user must have a pretty fast computer.
                    # time.time() - startTime equaled zero.
                    pass

                address = encodeAddress(
                    addressVersionNumber, streamNumber, ripe)

                # An excellent way for us to store our keys
                # is in Wallet Import Format. Let us convert now.
                # https://en.bitcoin.it/wiki/Wallet_import_format
                privSigningKey ='\x80'.encode('raw_unicode_escape') + potentialPrivSigningKey
                checksum = hashlib.sha256(hashlib.sha256(
                    privSigningKey).digest()).digest()[0:4]
                privSigningKeyWIF = arithmetic.changebase(
                    privSigningKey + checksum, 256, 58)

                privEncryptionKey ='\x80'.encode('raw_unicode_escape') + potentialPrivEncryptionKey
                checksum = hashlib.sha256(hashlib.sha256(
                    privEncryptionKey).digest()).digest()[0:4]
                privEncryptionKeyWIF = arithmetic.changebase(
                    privEncryptionKey + checksum, 256, 58)
                BMConfigParser().add_section(address)
                # BMConfigParser().set(address, 'label', label)
                BMConfigParser().set(address, 'enabled', 'true')
                BMConfigParser().set(address, 'decoy', 'false')
                BMConfigParser().set(address, 'noncetrialsperbyte', str(
                    nonceTrialsPerByte))
                BMConfigParser().set(address, 'payloadlengthextrabytes', str(
                    payloadLengthExtraBytes))
                BMConfigParser().set(
                    address, 'privsigningkey', privSigningKeyWIF)
                BMConfigParser().set(
                    address, 'privencryptionkey', privEncryptionKeyWIF)
                BMConfigParser().set(address, 'hidden', 'true')
                BMConfigParser().set(address, 'payment', 'true')
                BMConfigParser().save()

                # The API and the join and create Chan functionality
                # both need information back from the address generator.
                queues.apiAddressGeneratorReturnQueue.put(address)
                queues.UISignalQueue.put((
                    'updateStatusBar', ""
                ))
                queues.UISignalQueue.put(('writeNewpaymentAddressToTable', (
                    label, address, streamNumber)))
                shared.reloadMyAddressHashes()
                if addressVersionNumber == 3:
                    queues.workerQueue.put((
                        'sendOutOrStoreMyV3Pubkey', ripe))
                elif addressVersionNumber == 4:
                    queues.workerQueue.put((
                        'sendOutOrStoreMyV4Pubkey', address))

            elif command in (
                    'createDeterministicAddresses',
                    'getDeterministicAddress',
                    'createChan',
                    'joinChan'):
                logger.error('++++++++++++++387+++++++++++')
                if not deterministicPassphrase:
                    self.logger.warning(
                        'You are creating deterministic'
                        ' address(es) using a blank passphrase.'
                        ' Bitmessage will do it but it is rather stupid.')
                if command == 'createDeterministicAddresses':
                    queues.UISignalQueue.put((
                        'updateStatusBar',
                        tr._translate(
                            "MainWindow",
                            "Generating %1 new addresses."
                        ).arg(str(numberOfAddressesToMake))
                    ))
                logger.error('++++++++++401++++++++++++++')
                signingKeyNonce = 0
                encryptionKeyNonce = 1
                # We fill out this list no matter what although we only
                # need it if we end up passing the info to the API.
                logger.error('++++++++++406++++++++++++++')
                listOfNewAddressesToSendOutThroughTheAPI = []
                logger.error('++++++++++409++++++++++++++')
                for _ in range(numberOfAddressesToMake):
                    # This next section is a little bit strange. We're
                    # going to generate keys over and over until we find
                    # one that has a RIPEMD hash that starts with either
                    # \x00 or \x00\x00. Then when we pack them into a
                    # Bitmessage address, we won't store the \x00 or
                    # \x00\x00 bytes thus making the address shorter.
                    logger.error('++++++++++416++++++++++++++')
                    startTime = time.time()
                    logger.error('++++++++++418++++++++++++++')
                    numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix = 0
                    while True:
                        logger.error('++++++++++421++++++++++++++')
                        numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix += 1
                        logger.error('++++++++++423++++++++++++++')
                        logger.error('signingKeyNonce  424 -{}+++++++'.format(
                            signingKeyNonce
                        ))
                        logger.error('encodeVarint(signingKeyNonce)  427 -{}+'.format(
                            encodeVarint(signingKeyNonce)
                        ))
                        logger.error('deterministicPassphrase  427 -{}+'.format(
                            deterministicPassphrase
                        ))
                        potentialPrivSigningKey = hashlib.sha512(
                            deterministicPassphrase.encode('raw_unicode_escape') +
                            encodeVarint(signingKeyNonce)
                        ).digest()[:32]
                        logger.error('++++++++++428++++++++++++++')
                        logger.error('++++++++++++429-{}+++++++++'.format(
                            encryptionKeyNonce
                        ))
                        potentialPrivEncryptionKey = hashlib.sha512(
                            deterministicPassphrase.encode('raw_unicode_escape') +
                            encodeVarint(encryptionKeyNonce)
                        ).digest()[:32]
                        logger.error('++++++++++433++++++++++++++')
                        potentialPubSigningKey = highlevelcrypto.pointMult(
                            potentialPrivSigningKey)
                        logger.error('++++++++++437++++++++++++++')
                        potentialPubEncryptionKey = highlevelcrypto.pointMult(
                            potentialPrivEncryptionKey)
                        logger.error('++++++++++439++++++++++++++')
                        signingKeyNonce += 2
                        logger.error('++++++++++441++++++++++++++')
                        encryptionKeyNonce += 2
                        logger.error('++++++++++443++++++++++++++')
                        sha = hashlib.new('sha512')
                        sha.update(
                            potentialPubSigningKey + potentialPubEncryptionKey)
                        logger.error('++++++++++447++++++++++++++')
                        ripe = RIPEMD160Hash(sha.digest()).digest()
                        logger.error('++++++++++449++++++++++++++')
                        if (
                            ripe[:numberOfNullBytesDemandedOnFrontOfRipeHash] ==
                            '\x00'.encode() * numberOfNullBytesDemandedOnFrontOfRipeHash
                        ):
                            logger.error('++++++++++454++++++++++++++')
                            break
                    logger.error('++++++++++418++++++++++++++')                    
                    self.logger.info(
                        'Generated address with ripe digest: %s', hexlify(ripe))
                    try:
                        logger.error('++++++++++460++++++++++++++')                    
                        self.logger.info(
                            'Address generator calculated %s addresses'
                            ' at %s addresses per second before finding'
                            ' one with the correct ripe-prefix.',
                            numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix,
                            numberOfAddressesWeHadToMakeBeforeWeFoundOneWithTheCorrectRipePrefix /
                            (time.time() - startTime)
                        )
                    except ZeroDivisionError:
                        logger.error('++++++++++470++++++++++++++')                    
                        
                        # The user must have a pretty fast computer.
                        # time.time() - startTime equaled zero.
                        pass
                    logger.error('++++++++++475++++++++++++++')                    
                    
                    address = encodeAddress(
                        addressVersionNumber, streamNumber, ripe)
                    logger.error('++++++++++479++++++++++++++')                    

                    saveAddressToDisk = True
                    # If we are joining an existing chan, let us check
                    # to make sure it matches the provided Bitmessage address
                    logger.error('++++++++++484++++++++++++++')                    
                    
                    if command == 'joinChan':
                        logger.error('++++++++++487++++++++++++++')                    
                        
                        if address != chanAddress:
                            logger.error('++++++++++490++++++++++++++')                    
                            
                            listOfNewAddressesToSendOutThroughTheAPI.append(
                                'chan name does not match address')
                            logger.error('++++++++++494++++++++++++++')                    
                            saveAddressToDisk = False
                    if command == 'getDeterministicAddress':
                        saveAddressToDisk = False
                        logger.error('++++++++++498++++++++++++++')                    
                        

                    if saveAddressToDisk and live:
                        logger.error('++++++++++501++++++++++++++')                    
                        
                        # An excellent way for us to store our keys is
                        # in Wallet Import Format. Let us convert now.
                        # https://en.bitcoin.it/wiki/Wallet_import_format
                        privSigningKey = '\x80'.encode('raw_unicode_escape') + potentialPrivSigningKey
                        logger.error('++++++++++508++++++++++++++')                    
                        
                        checksum = hashlib.sha256(hashlib.sha256(
                            privSigningKey).digest()).digest()[0:4]
                        logger.error('++++++++++512++++++++++++++')                    
                        privSigningKeyWIF = arithmetic.changebase(
                            privSigningKey + checksum, 256, 58)
                        logger.error('++++++++++515++++++++++++++')                    
                        privEncryptionKey = '\x80'.encode('raw_unicode_escape') + \
                            potentialPrivEncryptionKey
                        logger.error('++++++++++518++++++++++++++')                    
                        checksum = hashlib.sha256(hashlib.sha256(
                            privEncryptionKey).digest()).digest()[0:4]
                        logger.error('++++++++++521++++++++++++++')                    
                        privEncryptionKeyWIF = arithmetic.changebase(
                            privEncryptionKey + checksum, 256, 58)
                        logger.error('++++++++++524++++++++++++++')                    
                        try:
                            logger.error('++++++++++526++++++++++++++')                    
                            BMConfigParser().add_section(address)
                            addressAlreadyExists = False
                        except:
                            logger.error('++++++++++530++++++++++++++')                    
                            addressAlreadyExists = True

                        if addressAlreadyExists:
                            logger.error('++++++++++534++++++++++++++')                    
                            self.logger.info(
                                '%s already exists. Not adding it again.',
                                address
                            )
                            logger.error('++++++++++539++++++++++++++')                    
                            queues.UISignalQueue.put((
                                'updateStatusBar',
                                tr._translate(
                                    "MainWindow",
                                    "%1 is already in 'Your Identities'."
                                    " Not adding it again."
                                ).arg(address)
                            ))
                        else:
                            logger.error('++++++++++549++++++++++++++')                    
                            self.logger.debug('label: %s', label)
                            BMConfigParser().set(address, 'label', label)
                            BMConfigParser().set(address, 'enabled', 'true')
                            BMConfigParser().set(address, 'decoy', 'false')
                            logger.error('++++++++++554++++++++++++++')                    
                            # if command == 'joinChan' or command == 'createChan':
                            if command in ('joinChan', 'createChan'):
                                BMConfigParser().set(address, 'chan', 'true')
                                logger.error('++++++++++558++++++++++++++')                    
                            BMConfigParser().set(
                                address, 'noncetrialsperbyte',
                                str(nonceTrialsPerByte))
                            logger.error('++++++++++562++++++++++++++')                    
                            BMConfigParser().set(
                                address, 'payloadlengthextrabytes',
                                str(payloadLengthExtraBytes))
                            logger.error('++++++++++566++++++++++++++')                    
                            BMConfigParser().set(
                                address, 'privSigningKey',
                                privSigningKeyWIF)
                            logger.error('++++++++++570++++++++++++++')                    
                            BMConfigParser().set(
                                address, 'privEncryptionKey',
                                privEncryptionKeyWIF)
                            BMConfigParser().save()
                            logger.error('++++++++++575++++++++++++++')                    

                            queues.UISignalQueue.put((
                                'writeNewAddressToTable',
                                (label, address, str(streamNumber))
                            ))
                            logger.error('++++++++++581++++++++++++++')                    
                            listOfNewAddressesToSendOutThroughTheAPI.append(
                                address)
                            logger.error('++++++++++584++++++++++++++')                    
                            shared.myECCryptorObjects[ripe] = \
                                highlevelcrypto.makeCryptor(
                                    hexlify(potentialPrivEncryptionKey))
                            logger.error('++++++++++588++++++++++++++')                    
                            shared.myAddressesByHash[ripe] = address
                            tag = hashlib.sha512(hashlib.sha512(
                                encodeVarint(addressVersionNumber) +
                                encodeVarint(streamNumber) + ripe
                            ).digest()).digest()[32:]
                            logger.error('++++++++++594++++++++++++++')                    
                            shared.myAddressesByTag[tag] = address
                            if addressVersionNumber == 3:
                                logger.error('++++++++++597++++++++++++++')                    
                                
                                # If this is a chan address,
                                # the worker thread won't send out
                                # the pubkey over the network.
                                queues.workerQueue.put((
                                    'sendOutOrStoreMyV3Pubkey', ripe))
                            elif addressVersionNumber == 4:
                                logger.error('++++++++++605++++++++++++++')                    
                                queues.workerQueue.put((
                                    'sendOutOrStoreMyV4Pubkey', address))
                            queues.UISignalQueue.put((
                                'updateStatusBar',
                                tr._translate(
                                    "MainWindow", "Done generating address")
                            ))
                    elif saveAddressToDisk and not live \
                            and not BMConfigParser().has_section(address):
                        listOfNewAddressesToSendOutThroughTheAPI.append(
                            address)

                # Done generating addresses.
                # if command == 'createDeterministicAddresses' \
                #         or command == 'joinChan' or command == 'createChan':
                logger.error('++++++++++621++++++++++++++')                    
                if command in (
                        'createDeterministicAddresses',
                        'joinChan',
                        'createChan'):
                    logger.error('++++++++++++++626+++++++++++')
                    queues.apiAddressGeneratorReturnQueue.put(
                        listOfNewAddressesToSendOutThroughTheAPI)
                elif command == 'getDeterministicAddress':
                    queues.apiAddressGeneratorReturnQueue.put(address)
            else:
                logger.info("Error in the addressGenerator thread. Thread was" +
                    " given a command it could not understand:{} " .format(command))
                raise Exception(
                    "Error in the addressGenerator thread. Thread was" +
                    " given a command it could not understand: " + command)
            queues.addressGeneratorQueue.task_done()
